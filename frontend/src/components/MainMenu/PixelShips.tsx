import { useEffect, useRef, useState } from 'react';
import './PixelShips.css';

type Ship = {
  x: number;
  y: number;
  speed: number;
  type: number;
  color: string;
  sinking?: boolean;
  sinkProgress?: number;
};
const shipCount = 20;

const PixelShips = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [ships, setShips] = useState<Ship[]>([]);

  useEffect(() => {
    const canvas = canvasRef.current!;
    const ctx = canvas.getContext('2d')!;
    
    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Яркие цвета кораблей
    const shipColors = ['#4a8dac', '#3a7d9c', '#2c6d8c'];
    const shipTypes = [
      { width: 50, height: 12, tower: { x: 15, y: -10, width: 10, height: 10 } },
      { width: 30, height: 8, tower: { x: 10, y: -8, width: 8, height: 8 } },
      { width: 20, height: 6, tower: null }
    ];

    // Инициализация кораблей
    const initShips = () => {
      const newShips: Ship[] = Array(shipCount).fill(0).map(() => ({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height * 0.7 + canvas.height * 0.1,
        speed: 0.2 + Math.random() * 0.8,
        type: Math.floor(Math.random() * shipTypes.length),
        color: shipColors[Math.floor(Math.random() * shipColors.length)],
        sinking: false,
        sinkProgress: 0
      }));
      setShips(newShips);
      return newShips;
    };

    let shipsData = initShips();
    let lastTime = 0;
    const sinkInterval = 3000; // Каждые 3 секунды тонет случайный корабль

    const drawShip = (ship: Ship) => {
      const { width, height, tower } = shipTypes[ship.type];
      const y = ship.sinking ? ship.y + ship.sinkProgress! * 2 : ship.y;
      
      // Корпус
      ctx.fillStyle = ship.color;
      ctx.fillRect(ship.x, y, width, height);
      
      // Башня
      if (tower) {
        ctx.fillRect(ship.x + tower.x, y + tower.y, tower.width, tower.height);
      }
      
      // Огоньки
      ctx.fillStyle = '#00f7ff';
      for (let i = 0; i < 3; i++) {
        ctx.fillRect(ship.x + 5 + i*10, y + 2, 3, 3);
      }

      // Взрыв при потоплении
      if (ship.sinking) {
        const explosionSize = ship.sinkProgress! * 30;
        ctx.fillStyle = `rgba(255, ${100 + ship.sinkProgress! * 50}, 0, ${1 - ship.sinkProgress!})`;
        ctx.beginPath();
        ctx.arc(ship.x + width/2, y + height/2, explosionSize, 0, Math.PI * 2);
        ctx.fill();
      }
    };

    const animate = (time: number) => {
      if (!lastTime) lastTime = time;
      const delta = time - lastTime;
      lastTime = time;

      ctx.clearRect(0, 0, canvas.width, canvas.height);

      const gradient = ctx.createLinearGradient(0, 0, 0, window.innerHeight);
      gradient.addColorStop(0, '#000b28');
      gradient.addColorStop(0.5, '#003a6b');
      gradient.addColorStop(1, '#002140');
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, window.innerWidth, window.innerHeight);
      
      // Волны
    //   ctx.fillStyle = 'rgba(0, 200, 255, 0.1)';
    //   for (let i = 0; i < 5; i++) {
    //     const waveY = canvas.height * 0.8 + Math.sin(time * 0.001 + i) * 5;
    //     ctx.fillRect(0, waveY, canvas.width, 2);
    //   }

      // Обновляем корабли
      shipsData = shipsData.map(ship => {
        if (ship.sinking) {
          return {
            ...ship,
            sinkProgress: Math.min(1, (ship.sinkProgress || 0) + delta / 1000)
          };
        }
        return {
          ...ship,
          x: ship.x + ship.speed
        };
      }).filter(ship => !ship.sinking || ship.sinkProgress! < 1);

      // Добавляем новые корабли вместо потопленных
      while (shipsData.length < shipCount) {
        shipsData.push({
          x: -50,
          y: Math.random() * canvas.height * 0.7 + canvas.height * 0.1,
          speed: 0.2 + Math.random() * 0.8,
          type: Math.floor(Math.random() * shipTypes.length),
          color: shipColors[Math.floor(Math.random() * shipColors.length)],
          sinking: false
        });
      }

      // Потопление случайного корабля
      if (time % sinkInterval < delta) {
        const aliveShips = shipsData.filter(s => !s.sinking);
        if (aliveShips.length > 0) {
          const victimIndex = Math.floor(Math.random() * aliveShips.length);
          shipsData = shipsData.map((ship, i) => 
            i === shipsData.indexOf(aliveShips[victimIndex]) 
              ? { ...ship, sinking: true, sinkProgress: 0 } 
              : ship
          );
        }
      }

      // Рисуем корабли
      shipsData.forEach(drawShip);
      requestAnimationFrame(animate);
    };

    const animationId = requestAnimationFrame(animate);

    return () => {
      cancelAnimationFrame(animationId);
      window.removeEventListener('resize', resizeCanvas);
    };
  }, []);

  return <canvas ref={canvasRef} className="pixel-ships" />;
};

export default PixelShips;