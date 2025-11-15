'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useLogin } from '../../../hooks/use-login';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const router = useRouter();
  const { mutate: login, isPending, error } = useLogin();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    login(
      { email, password },
      {
        onSuccess: (data) => {
          localStorage.setItem('accessToken', data.accessToken);
          localStorage.setItem('refreshToken', data.refreshToken);
          router.push('/');
        },
      }
    );
  };

  return (
    <div className="w-full max-w-md">
      <div className="bg-white dark:bg-slate-950 rounded-lg shadow-lg p-8 space-y-8">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-slate-900 dark:text-white">Welcome Back</h1>
          <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">Sign in to continue to your account</p>
        </div>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <input
              id="email"
              name="email"
              type="email"
              autoComplete="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-3 text-slate-900 dark:text-white border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400"
              placeholder="Email address"
            />
          </div>
          <div>
            <input
              id="password"
              name="password"
              type="password"
              autoComplete="current-password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-3 text-slate-900 dark:text-white border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400"
              placeholder="Password"
            />
          </div>
          {error && <p className="text-sm text-red-600 dark:text-red-400">{(error as any).message}</p>}
          <div>
            <button
              type="submit"
              disabled={isPending}
              className="w-full px-4 py-3 font-semibold text-white bg-blue-600 dark:bg-blue-700 rounded-lg shadow-md hover:bg-blue-700 dark:hover:bg-blue-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
            >
              {isPending ? 'Signing in...' : 'Sign in'}
            </button>
          </div>
        </form>
        <div className="text-sm text-center text-slate-600 dark:text-slate-400">
          {"Don't have an account? "}
          <Link href="/register" className="font-medium text-blue-600 dark:text-blue-400 hover:underline">
            Sign up
          </Link>
        </div>
      </div>
    </div>
  );
}

