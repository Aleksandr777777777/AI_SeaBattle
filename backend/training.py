def compute_reward(result, game_over):
    if result == "hit":
        return 1.0
    elif result == "sink":
        return 5.0
    elif result == "miss":
        return -1.0
    if game_over:
        # Если игра окончена и мы выиграли:
        return 50.0
    return 0.0

def train_dqn_agent(episodes=10000):
    from agent import RLAgent
    agent = RLAgent()
    
    for ep in range(episodes):
        game = Game()
        agent.start_new_game()
        done = False
        while not done:
            # Формируем состояние
            state = agent.get_state(game)

            # Решаем, переключать ли стратегию
            action = agent.select_action(state)
            agent.apply_action(action)

            # Делаем выстрел
            row, col = agent.get_next_shot(game)
            result, done = game.make_move(row, col)

            # Считаем награду
            reward = compute_reward(result, done)
            
            # Новое состояние
            next_state = agent.get_state(game)
            agent.remember(state, action, reward, next_state, float(done))

            # Сохраняем результат выстрела
            agent.on_shot_result(row, col, result, game)
            
            # Если промах, передаём ход сопернику
            # (если есть AI vs AI, нужно аналогично вызывать логику для второго агента)
            # ...

            agent.learn()

        # Можно вывести статистику
        if ep % 100 == 0:
            print(f"Episode {ep}/{episodes} done")

    # По завершении сохранить веса
    torch.save(agent.policy_net.state_dict(), "dqn_agent.pth")
