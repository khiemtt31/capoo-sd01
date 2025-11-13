"use client";

import { z } from "zod";
import { ReactNode, createContext, useState, useContext, useMemo } from "react";

const userSchema = z.object({
  id: z.string(),
  username: z.string(),
  email: z.string().email(),
});

export type User = z.infer<typeof userSchema>;

interface UserContextType {
  user: User | null;
  login: (userData: User) => void;
  logout: () => void;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

export const UserProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);

  const login = (userData: User) => {
    const validatedUser = userSchema.parse(userData);
    setUser(validatedUser);
  };

  const logout = () => {
    setUser(null);
  };

  const value = useMemo(
    () => ({
      user,
      login,
      logout,
    }),
    [user]
  );

  return <UserContext.Provider value={value}>{children}</UserContext.Provider>;
};

export const useUser = () => {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error("useUser must be used within a UserProvider");
  }
  return context;
};