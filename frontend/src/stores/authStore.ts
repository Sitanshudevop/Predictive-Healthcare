import { create } from "zustand";

interface User {
  id: number;
  email: string;
  name: string;
  role: string;
}

interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  login: (user: User, token: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  // Soft bypass: Hardcoded to always be authenticated as Guest User
  isAuthenticated: true,
  user: {
    id: 1,
    email: "guest@predictivehealthcare.com",
    name: "Guest User",
    role: "user"
  },
  login: (user, token) => {
    // No-op for soft bypass
  },
  logout: () => {
    // No-op for soft bypass
  },
}));
