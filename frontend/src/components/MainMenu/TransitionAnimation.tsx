import { useEffect, useRef } from 'react';
import './TransitionAnimation.css';

const TransitionAnimation = ({ onComplete }: { onComplete: () => void }) => {
  const overlayRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Получаем цвета из CSS переменных
    const rootStyles = getComputedStyle(document.documentElement);
    const colorStart = rootStyles.getPropertyValue('--transition-start') || '#004e92';
    const colorEnd = rootStyles.getPropertyValue('--transition-end') || '#000428';

    // Установка размеров
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const centerX = canvas.width;
    const centerY = canvas.height;
    const maxRadius = Math.sqrt(centerX ** 2 + centerY ** 2);
    const duration = 1000;
    let startTime: number;

    const animate = (currentTime: number) => {
      if (!startTime) startTime = currentTime;
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);

      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      // Создаем градиент
      const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
      gradient.addColorStop(0, colorStart);
      gradient.addColorStop(1, colorEnd);
      ctx.fillStyle = gradient;
      
      // Рисуем волну
      ctx.beginPath();
      const radius = progress * maxRadius;
      const waveCount = 4;
      
      for (let angle = 0; angle <= Math.PI * 2; angle += 0.02) {
        const waveOffset = Math.sin(angle * waveCount + progress * Math.PI * 6) * 30;
        const x = centerX + Math.cos(angle) * (radius + waveOffset);
        const y = centerY + Math.sin(angle) * (radius + waveOffset);
        angle === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
      }
      
      ctx.closePath();
      ctx.fill();

      if (progress < 1) {
        requestAnimationFrame(animate);
      } else {
        setTimeout(onComplete, 200);
      }
    };

    setTimeout(() => {
      startTime = performance.now();
      requestAnimationFrame(animate);
    }, 300);

    return () => ctx.clearRect(0, 0, canvas.width, canvas.height);
  }, [onComplete]);

  return (
    <div ref={overlayRef} className="transition-overlay">
      <canvas ref={canvasRef} className="transition-canvas" />
    </div>
  );
};

export default TransitionAnimation;