interface ProgressBarProps {
  current: number;
  total: number;
}

export const ProgressBar = ({ current, total }: ProgressBarProps) => {
  const percentage = (current / total) * 100;
  
  return (
    <div className="w-full bg-secondary rounded-full h-2 overflow-hidden">
      <div
        className="h-full bg-primary animate-progress-fill"
        style={{ "--progress-width": `${percentage}%` } as React.CSSProperties}
      />
    </div>
  );
};