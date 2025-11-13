import { useMutation } from '@tanstack/react-query';
import { login } from '../api/auth';
import { LoginForm } from '../api/types';

export const useLogin = () => {
  return useMutation({
    mutationFn: (data: LoginForm) => login(data),
  });
};