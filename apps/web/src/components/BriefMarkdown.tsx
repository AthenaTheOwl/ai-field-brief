import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface BriefMarkdownProps {
  source: string;
}

/**
 * Renders the body of a brief into prose. Strips the leading H1 so the page
 * template owns the title rendering.
 */
export function BriefMarkdown({ source }: BriefMarkdownProps) {
  const body = source.replace(/^#\s+.+?\n+/, "");
  return (
    <article className="prose prose-neutral prose-lg dark:prose-invert max-w-none">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          a: ({ href, children, ...rest }) => (
            <a
              href={href}
              target={href?.startsWith("http") ? "_blank" : undefined}
              rel={href?.startsWith("http") ? "noopener noreferrer" : undefined}
              {...rest}
            >
              {children}
            </a>
          ),
        }}
      >
        {body}
      </ReactMarkdown>
    </article>
  );
}
