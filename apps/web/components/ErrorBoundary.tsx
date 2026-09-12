"use client";

import React, { Component, ErrorInfo, ReactNode } from "react";

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
    errorInfo: null,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error, errorInfo: null };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    this.setState({ error, errorInfo });
    console.error("ZAYVORA Clinical UI ErrorBoundary caught error:", error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <div className="min-h-[400px] flex flex-col items-center justify-center p-8 bg-amber-50 border border-amber-200 rounded-2xl shadow-sm text-slate-800 m-4">
          <div className="w-16 h-16 rounded-full bg-amber-100 flex items-center justify-center text-amber-700 text-3xl font-bold mb-4">
            ⚠️
          </div>
          <h2 className="text-xl font-bold text-slate-900 mb-2">
            Clinical Service Communication Error
          </h2>
          <p className="text-sm text-slate-600 max-w-lg text-center mb-4">
            A network or upstream microservice failure occurred. In adherence to ZAYVORA Clinical Governance,
            provisional mock data is never silently displayed in production mode.
          </p>
          {this.state.error && (
            <div className="bg-white border border-amber-300 rounded-lg p-3 max-w-xl w-full text-xs font-mono text-red-700 overflow-x-auto mb-6">
              {this.state.error.name}: {this.state.error.message}
            </div>
          )}
          <div className="flex gap-3">
            <button
              onClick={() => this.setState({ hasError: false, error: null, errorInfo: null })}
              className="px-4 py-2 bg-emerald-700 hover:bg-emerald-800 text-white text-sm font-semibold rounded-lg shadow-sm transition-colors"
            >
              Retry Action
            </button>
            <button
              onClick={() => window.location.reload()}
              className="px-4 py-2 bg-slate-200 hover:bg-slate-300 text-slate-700 text-sm font-medium rounded-lg transition-colors"
            >
              Reload Page
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
