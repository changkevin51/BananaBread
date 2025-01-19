import { cn } from "@/lib/utils";

interface ChatMessageProps {
  content: string;
  isAI: boolean;
  animate?: boolean;
}

export const ChatMessage = ({ content, isAI, animate = true }: ChatMessageProps) => {
  return (
    <div
      className={cn(
        "max-w-[80%] rounded-2xl px-4 py-2 mb-2",
        isAI ? "bg-chat-ai/10 mr-auto" : "bg-chat-user/10 ml-auto",
        animate && "animate-fade-in"
      )}
    >
      <p className="text-sm">{content}</p>
    </div>
  );
};