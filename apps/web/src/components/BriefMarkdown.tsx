import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface BriefMarkdownProps {
  source: string;
}

/**
 * Renders the body of a brief into prose. Strips publish metadata and the
 * leading H1 so the page template owns the title rendering.
 */
export function stripBriefChrome(source: string): string {
  return source
    .replace(/^\s*<!--[\s\S]*?-->\s*/, "")
    .replace(/^#\s+.+?\n+/, "");
}

export function BriefMarkdown({ source }: BriefMarkdownProps) {
  const body = stripBriefChrome(source);
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
          table: ({ children, ...rest }) => (
            <div className="my-8 max-w-full overflow-x-auto">
              <table className="min-w-[44rem]" {...rest}>
                {children}
              </table>
            </div>
          ),
        }}
      >
        {body}
      </ReactMarkdown>
    </article>
  );
}
