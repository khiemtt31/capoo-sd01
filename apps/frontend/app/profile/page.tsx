'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useProfile, useUpdateProfile } from '../../hooks/use-profile';

export default function ProfilePage() {
  const router = useRouter();
  const { data: user, isLoading, error } = useProfile();
  const { mutate: updateProfile, isPending: isUpdating } = useUpdateProfile();
  const [name, setName] = useState('');
  const [avatar, setAvatar] = useState('');

  useEffect(() => {
    if (user) {
      setName(user.name);
      setAvatar(user.avatar);
    }
  }, [user]);

  const handleUpdate = (e: React.FormEvent) => {
    e.preventDefault();
    updateProfile(
      { name, avatar },
      {
        onSuccess: () => {
          alert('Profile updated successfully!');
        },
      }
    );
  };

  if (isLoading) {
    return <div className="flex items-center justify-center min-h-screen">Loading...</div>;
  }

  if (error) {
    return <div className="flex items-center justify-center min-h-screen text-red-600">{error.message}</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="container mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900">Your Profile</h1>
        </div>
      </header>
      <main className="container mx-auto px-4 py-8">
        <div className="w-full max-w-2xl p-8 mx-auto space-y-8 bg-white rounded-xl shadow-lg">
          {user && (
            <form onSubmit={handleUpdate} className="space-y-6">
              <div className="flex items-center space-x-6">
                <img
                  src={avatar || `https://ui-avatars.com/api/?name=${user.name}&background=random`}
                  alt="Avatar"
                  className="w-24 h-24 rounded-full"
                />
                <div className="flex-1">
                  <label htmlFor="avatar" className="block text-sm font-medium text-gray-700">
                    Avatar URL
                  </label>
                  <input
                    id="avatar"
                    type="text"
                    value={avatar}
                    onChange={(e) => setAvatar(e.target.value)}
                    className="w-full px-4 py-3 mt-1 text-gray-900 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="https://example.com/avatar.png"
                  />
                </div>
              </div>
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                  Name
                </label>
                <input
                  id="name"
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full px-4 py-3 mt-1 text-gray-900 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                  Email
                </label>
                <input
                  id="email"
                  type="email"
                  value={user.email}
                  disabled
                  className="w-full px-4 py-3 mt-1 text-gray-500 bg-gray-100 border border-gray-300 rounded-lg"
                />
              </div>
              <div>
                <button
                  type="submit"
                  disabled={isUpdating}
                  className="w-full px-4 py-3 font-semibold text-white bg-blue-600 rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  {isUpdating ? 'Updating...' : 'Update Profile'}
                </button>
              </div>
            </form>
          )}
        </div>
      </main>
    </div>
  );
}