/**
 * Card — ZAYVORA Design System
 *
 * A composable surface container with optional header, body, and footer
 * slots. Supports a shadow elevation variant.
 *
 * @module design-system/Card
 */

import React, { HTMLAttributes } from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

// ─────────────────────────────────────────────────────────────────────────────
// Types
// ─────────────────────────────────────────────────────────────────────────────

export type CardShadow = 'none' | 'sm' | 'md' | 'lg';

export interface CardProps extends HTMLAttributes<HTMLDivElement> {
  /** Shadow elevation level. Defaults to "md". */
  shadow?: CardShadow;
  /** Add a subtle hover-lift effect. */
  hoverable?: boolean;
  /** Remove internal padding (useful when embedding images or full-bleed content). */
  noPadding?: boolean;
}

export interface CardHeaderProps extends HTMLAttributes<HTMLDivElement> {
  /** Supplementary action placed in the top-right of the header. */
  action?: React.ReactNode;
}

export interface CardSectionProps extends HTMLAttributes<HTMLDivElement> {}

// ─────────────────────────────────────────────────────────────────────────────
// Style maps
// ─────────────────────────────────────────────────────────────────────────────

const shadowClasses: Record<CardShadow, string> = {
  none: 'shadow-none',
  sm:   'shadow-card',
  md:   'shadow-[0_1px_3px_0_rgb(0_0_0/0.08),0_1px_2px_-1px_rgb(0_0_0/0.06)]',
  lg:   'shadow-[0_4px_12px_0_rgb(0_0_0/0.12),0_2px_4px_-1px_rgb(0_0_0/0.08)]',
};

// ─────────────────────────────────────────────────────────────────────────────
// Sub-components
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Card.Header — top section with an optional action slot.
 */
const CardHeader: React.FC<CardHeaderProps> = ({
  children,
  action,
  className,
  ...rest
}) => (
  <div
    className={twMerge(
      clsx(
        'flex items-start justify-between gap-4',
        'px-5 py-4 border-b border-gray-100',
      ),
      className,
    )}
    {...rest}
  >
    <div className="flex-1 min-w-0">{children}</div>
    {action && <div className="shrink-0">{action}</div>}
  </div>
);

CardHeader.displayName = 'Card.Header';

/**
 * Card.Body — main content area.
 */
const CardBody: React.FC<CardSectionProps> = ({
  children,
  className,
  ...rest
}) => (
  <div
    className={twMerge(clsx('px-5 py-4 flex-1'), className)}
    {...rest}
  >
    {children}
  </div>
);

CardBody.displayName = 'Card.Body';

/**
 * Card.Footer — bottom section, typically for actions.
 */
const CardFooter: React.FC<CardSectionProps> = ({
  children,
  className,
  ...rest
}) => (
  <div
    className={twMerge(
      clsx(
        'px-5 py-3 border-t border-gray-100',
        'bg-[#F3F3EE] rounded-b-xl',
        'flex items-center gap-3',
      ),
      className,
    )}
    {...rest}
  >
    {children}
  </div>
);

CardFooter.displayName = 'Card.Footer';

// ─────────────────────────────────────────────────────────────────────────────
// Root Card component
// ─────────────────────────────────────────────────────────────────────────────

type CardComponent = React.FC<CardProps> & {
  Header: typeof CardHeader;
  Body:   typeof CardBody;
  Footer: typeof CardFooter;
};

/**
 * Card component.
 *
 * @example
 * <Card shadow="md" hoverable>
 *   <Card.Header action={<Button size="sm">Edit</Button>}>
 *     <h3 className="font-semibold text-[#1A1A1A]">Patient Summary</h3>
 *   </Card.Header>
 *   <Card.Body>…content…</Card.Body>
 *   <Card.Footer>
 *     <Button variant="ghost" size="sm">Cancel</Button>
 *   </Card.Footer>
 * </Card>
 */
const Card: CardComponent = ({
  shadow    = 'md',
  hoverable = false,
  noPadding = false,
  children,
  className,
  ...rest
}) => (
  <div
    className={twMerge(
      clsx(
        'bg-[#FAFAF7] rounded-xl border border-gray-100',
        'flex flex-col overflow-hidden',
        shadowClasses[shadow],
        !noPadding && 'divide-y divide-gray-100',
        hoverable && [
          'transition-shadow duration-200 cursor-pointer',
          'hover:shadow-[0_4px_12px_0_rgb(0_0_0/0.12),0_2px_4px_-1px_rgb(0_0_0/0.08)]',
        ],
        className,
      ),
    )}
    {...rest}
  >
    {children}
  </div>
);

Card.Header = CardHeader;
Card.Body   = CardBody;
Card.Footer = CardFooter;
Card.displayName = 'Card';

export { Card };
export default Card;
