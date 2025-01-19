import { Flame } from "lucide-react";

interface StreakCounterProps {
  streak: number;
}

export const StreakCounter = ({ streak }: StreakCounterProps) => {
  return (
    <div className="flex items-center gap-1 bg-orange-100 px-3 py-1 rounded-full">
      <Flame className="w-4 h-4 text-orange-500" />
      <span className="text-sm font-medium text-orange-700">{streak}</span>
    </div>
  );
};