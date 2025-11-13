import apiClient from './api-client';
import { LoginForm, RegisterForm } from './types';

export const login = async (data: LoginForm) => {
  const response = await apiClient.post('/auth/login', data);
  return response.data;
};

export const register = async (data: RegisterForm) => {
  const response = await apiClient.post('/auth/register', data);
  return response.data;
};