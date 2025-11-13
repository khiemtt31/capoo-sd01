import apiClient from './api-client';
import { User } from './types';

export const getProfile = async (): Promise<User> => {
  const response = await apiClient.get('/user/profile');
  return response.data;
};

export const updateProfile = async (data: Partial<User>): Promise<User> => {
  const response = await apiClient.put('/user/profile', data);
  return response.data;
};