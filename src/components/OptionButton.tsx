import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface OptionButtonProps {
  option: string;
  onClick: () => void;
  disabled?: boolean;
  isCorrect?: boolean | null;
}

export const OptionButton = ({ option, onClick, disabled, isCorrect }: OptionButtonProps) => {
  return (
    <Button
      className={cn(
        "w-full text-left justify-start",
        isCorrect === true && "bg-green-500 hover:bg-green-600",
        isCorrect === false && "bg-red-500 hover:bg-red-600"
      )}
      onClick={onClick}
      disabled={disabled}
    >
      {option}
    </Button>
  );
};