import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

from model import DQNNetwork
from strategies import ALL_PATTERNS
from finisher import ShipFinisher
#from ship_finisher import update_finishing_targets

class ReplayBuffer:
    def __init__(self, capacity=10000):
        self.buffer = []
        self.capacity = capacity
        self.index = 0

    def push(self, transition):
        # transition: (state, action, reward, next_state, done)
        if len(self.buffer) < self.capacity:
            self.buffer.append(None)
        self.buffer[self.index] = transition
        self.index = (self.index + 1) % self.capacity

    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)

    def __len__(self):
        return len(self.buffer)

class RLAgent:
    """
    Гибридный агент: 
    - При попадании "добивает" корабль по жёстким правилам
    - Для поиска использует одну из 4 стратегий (паттернов)
    - DQN учится решать, когда переключать паттерн, а когда оставаться
    """
    def __init__(self, 
                 state_dim=3, 
                 action_dim=5, 
                 lr=1e-3, 
                 gamma=0.99,
                 epsilon_start=1.0,
                 epsilon_end=0.01,
                 epsilon_decay=10000,
                 batch_size=64,
                 replay_size=10000):

        self.state_dim = state_dim
        self.action_dim = action_dim
        self.gamma = gamma
        self.batch_size = batch_size

        self.epsilon = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay = epsilon_decay
        self.step_count = 0
        self.current_hits = []
        self.shots_done = set() 
        self.finisher = ShipFinisher()



        self.policy_net = DQNNetwork(state_dim, action_dim)
        self.target_net = DQNNetwork(state_dim, action_dim)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()

        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=lr)
        self.replay_buffer = ReplayBuffer(capacity=replay_size)

        # Текущая стратегия
        self.patterns = ALL_PATTERNS
        self.current_pattern = None
        self.pattern_index = 0

        # Набор отстрелянных клеток
        self.shots_done = set()
        # Стек для "добивания"
        self.to_finish = []

        self.current_strategy_id = 0  # индекс [0..3] в ALL_PATTERNS

    def start_new_game(self):
        """
        Сбрасываем все внутренние данные агента для новой партии.
        """
        self.current_strategy_id = random.randint(0, len(self.patterns) - 1)
        self.current_pattern = self.patterns[self.current_strategy_id]
        self.pattern_index = 0
        self.shots_done.clear()
        self.to_finish.clear()
        self.current_hits.clear()


    def get_state(self, game):
        """
        Формируем вектор состояния:
         - осталось_непроверенных_клеток
         - осталось_палуб_у_противника
         - id_текущей_стратегии
        """
        unshot_cells = 0
        for r in range(10):
            for c in range(10):
                if game.board2[r][c] in [0,1]:  # 0=пусто,1=корабль (неизвестная/необстрелянная)
                    unshot_cells += 1

        ships_left = game.ships2  # допустим, в Game есть ships2 (кол-во живых палуб)
        strategy_id = self.current_strategy_id
        return np.array([unshot_cells, ships_left, strategy_id], dtype=np.float32)

    def select_action(self, state):
        """
        Выбираем действие (0=остаться, 1..4=переключиться на другую стратегию)
        \epsilon-greedy над Q-сетью
        """
        self.step_count += 1
        self.epsilon = max(self.epsilon_end, 
                           self.epsilon - (1.0 - self.epsilon_end)/self.epsilon_decay)

        if random.random() < self.epsilon:
            return random.randint(0, self.action_dim - 1)
        else:
            with torch.no_grad():
                s = torch.tensor(state, dtype=torch.float).unsqueeze(0)
                q_values = self.policy_net(s)
                return int(q_values.argmax().item())

    def apply_action(self, action):
        """
        Применяем действие:
         - A0: остаёмся на текущем паттерне
         - A1..A4: переключаемся на соответствующий паттерн
        """
        if action == 0:
            # Остаться
            return
        else:
            # Переключиться
            idx = action - 1  # если action=1 => idx=0 => patterns[0]
            if idx >= len(self.patterns):
                idx = len(self.patterns) - 1  # на всякий случай
            self.current_strategy_id = idx
            self.current_pattern = self.patterns[idx]
            self.pattern_index = 0

    def get_next_shot(self, game):
        """
        Возвращает (row, col) для выстрела.
        Если есть раненый корабль, "добиваем". Иначе идём по паттерну.
        """
        # 1. Добиваем
        next_shot = self.finisher.get_next_shot()
        if next_shot:
            if next_shot not in self.shots_done:  # Защита от дублей
                self.shots_done.add(next_shot)
                return next_shot
            else:
                return self.get_next_shot(game)

        # 2. Иначе идём по паттерну
        # print('Pattern_index', self.pattern_index)
        # print('Current_pattern', self.current_pattern)
        while self.pattern_index < len(self.current_pattern):
            r, c = self.current_pattern[self.pattern_index]
            self.pattern_index += 1
            if (r,c) not in self.shots_done:
                self.shots_done.add((r,c))
                return (r,c)

        # Если паттерн исчерпан, переключаемся случайно
        self.current_strategy_id = random.randint(0, len(self.patterns)-1)
        self.current_pattern = self.patterns[self.current_strategy_id]
        self.pattern_index = 0
        return self.get_next_shot(game)

    def on_shot_result(self, row, col, result, game):
        """
        Обработка результата выстрела.
        """
        self.shots_done.add((row, col))  # Всегда добавляем выстрел в трекер
        if result in ["hit", "sink"]:
            self.finisher.add_shot_result(row, col, result, board_size=10)
        if result == "sink":
            self.finisher.reset()
            # Можно добавить очистку клеток вокруг потопленного корабля
            self._mark_sunk_ship_neighbors(row, col, game)
    
    def _mark_sunk_ship_neighbors(self, row, col, game):
        """Помечает клетки вокруг потопленного корабля как 'использованные'."""
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < 10 and 0 <= nc < 10:
                    self.shots_done.add((nr, nc))

    def remember(self, state, action, reward, next_state, done):
        """
        Сохраняем переход в буфер
        """
        self.replay_buffer.push((state, action, reward, next_state, done))

    def learn(self):
        """
        Обновляем Q-сеть (DQN) из батча
        """
        if len(self.replay_buffer) < self.batch_size:
            return

        batch = self.replay_buffer.sample(self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        states = torch.tensor(states, dtype=torch.float)
        actions = torch.tensor(actions, dtype=torch.long).unsqueeze(1)
        rewards = torch.tensor(rewards, dtype=torch.float).unsqueeze(1)
        next_states = torch.tensor(next_states, dtype=torch.float)
        dones = torch.tensor(dones, dtype=torch.float).unsqueeze(1)

        # Q(s,a) = policy_net(s)[a]
        q_values = self.policy_net(states).gather(1, actions)

        # Q_target = r + gamma * max_a Q_target(next_s,a) (если not done)
        with torch.no_grad():
            next_q = self.target_net(next_states).max(1)[0].unsqueeze(1)
            q_target = rewards + (1 - dones) * self.gamma * next_q

        loss = nn.MSELoss()(q_values, q_target)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # Периодически обновляем target_net
        if self.step_count % 1000 == 0:
            self.target_net.load_state_dict(self.policy_net.state_dict())
