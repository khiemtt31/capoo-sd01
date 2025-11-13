export interface LoginForm {
  email: string;
  password?: string;
}

export interface RegisterForm {
  email: string;
  password?: string;
  confirmPassword?: string;
}

export interface User {
  id: string;
  email: string;
  name: string;
  avatar: string;
}