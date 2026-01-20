'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';
import { CheckSquare } from 'lucide-react';
import Link from 'next/link';

export default function HomePage() {
  const router = useRouter();

  useEffect(() => {
    // If user is already logged in, redirect to dashboard
    if (api.getToken()) {
      router.push('/dashboard');
    }
  }, [router]);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4">
      <div className="text-center max-w-md">
        <div className="flex justify-center mb-6">
          <div className="p-4 bg-primary-100 rounded-full">
            <CheckSquare className="w-12 h-12 text-primary-600" />
          </div>
        </div>

        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Task Manager
        </h1>

        <p className="text-lg text-gray-600 mb-8">
          Stay organized and boost your productivity with our simple and powerful task management app.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            href="/auth/login"
            className="px-6 py-3 bg-primary-600 text-white font-medium rounded-lg hover:bg-primary-700 transition-colors"
          >
            Sign In
          </Link>
          <Link
            href="/auth/signup"
            className="px-6 py-3 bg-white text-primary-600 font-medium rounded-lg border-2 border-primary-600 hover:bg-primary-50 transition-colors"
          >
            Create Account
          </Link>
        </div>

        <div className="mt-12 grid grid-cols-3 gap-6 text-center">
          <div>
            <div className="text-2xl font-bold text-primary-600">Easy</div>
            <div className="text-sm text-gray-500">to use</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-primary-600">Fast</div>
            <div className="text-sm text-gray-500">& reliable</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-primary-600">Secure</div>
            <div className="text-sm text-gray-500">& private</div>
          </div>
        </div>
      </div>
    </div>
  );
}
