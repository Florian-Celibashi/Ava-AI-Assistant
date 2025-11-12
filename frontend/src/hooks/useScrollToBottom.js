import { useEffect } from 'react';

/**
 * Scrolls to the bottom element when dependencies change and scrolling is enabled.
 */
export function useScrollToBottom(ref, dependencies = [], shouldScroll = true) {
  useEffect(() => {
    if (!shouldScroll) return;
    ref.current?.scrollIntoView({ behavior: 'smooth' });
  }, [...dependencies, shouldScroll]);
}
