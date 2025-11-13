import { useMutation } from '@tanstack/react-query';
import { register } from '../api/auth';
import { RegisterForm } from '../api/types';

export const useRegister = () => {
  return useMutation({
    mutationFn: (data: RegisterForm) => register(data),
  });
};