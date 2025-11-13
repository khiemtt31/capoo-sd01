import { useUser } from "@/core/user-context";

export const useAuth = () => {
  const { user, login, logout } = useUser();

  const isAuthenticated = !!user;

  return {
    user,
    login,
    logout,
    isAuthenticated,
  };
};