import { useEffect, useState, useRef } from "react";

export default function StartupNotice() {
    const [visible, setVisible] = useState(true);
    const [checking, setChecking] = useState(true);
    const retryRef = useRef(null);

    useEffect(() => {
        const controller = new AbortController();

        const ping = async () => {
            try {
                const res = await fetch((import.meta.env.VITE_BACKEND_URL || "") + "/", {
                    signal: controller.signal,
                });
                if (res.ok) {
                    setChecking(false);
                    // hide quickly once backend is ready
                    retryRef.current = setTimeout(() => setVisible(false), 300);
                } else {
                    throw new Error("Backend not ready");
                }
            } catch (e) {
                // retry until the backend wakes up (Render free cold start)
                retryRef.current = setTimeout(ping, 3000);
            }
        };

        ping();

        return () => {
            controller.abort();
            if (retryRef.current) clearTimeout(retryRef.current);
        };
    }, []);

    if (!visible || !checking) return null;

    return (
        <div
            aria-live="polite"
            aria-atomic="true"
            className="absolute bottom-24 left-1/2 -translate-x-1/2 z-40 pointer-events-none"
        >
            <div className="pointer-events-auto bg-white border border-gray-300 shadow-lg rounded-xl px-4 py-3 flex items-start gap-3 max-w-lg">
                {/* Spinner / status dot */}
                <svg
                    className="w-5 h-5 mt-0.5 text-blue-500 animate-spin"
                    viewBox="0 0 24 24"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                    aria-hidden="true"
                >
                    <circle cx="12" cy="12" r="9" stroke="currentColor" strokeWidth="2" opacity="0.2" />
                    <path d="M21 12a9 9 0 0 1-9 9" stroke="currentColor" strokeWidth="2" />
                </svg>

                <div className="text-sm leading-5 text-gray-700">
                    <p className="font-medium">
                        Note
                    </p>
                    <p className="text-gray-600">
                        Ava may take a few seconds to respond to the first inquiry as the server initializes. Subsequent responses are delivered promptly.
                    </p>
                </div>

                {/* Dismiss button */}
                <button
                    type="button"
                    className="ml-auto text-gray-400 hover:text-gray-600"
                    aria-label="Dismiss startup notice"
                    onClick={() => setVisible(false)}
                >
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
                        <path fillRule="evenodd" d="M6.225 4.811a1 1 0 011.414 0L12 9.172l4.361-4.361a1 1 0 111.414 1.414L13.414 10.586l4.361 4.361a1 1 0 01-1.414 1.414L12 12l-4.361 4.361a1 1 0 01-1.414-1.414l4.361-4.361-4.361-4.361a1 1 0 010-1.414z" clipRule="evenodd" />
                    </svg>
                </button>
            </div>
        </div>
    );
}