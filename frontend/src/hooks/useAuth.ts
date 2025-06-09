import { useState, useEffect } from "react";

interface User {
  id: string;
  email: string;
  name?: string;
}

interface AuthState {
  token: string | null;
  user: User | null;
  isLoading: boolean;
}

export const useAuth = () => {
  const [authState, setAuthState] = useState<AuthState>({
    token: null,
    user: null,
    isLoading: true,
  });

  useEffect(() => {
    const checkAuth = () => {
      try {
        const savedToken = localStorage.getItem("token");
        const savedUser = localStorage.getItem("user");

        if (savedToken) {
          const user = savedUser ? JSON.parse(savedUser) : null;
          setAuthState({
            token: savedToken,
            user,
            isLoading: false,
          });
        } else {
          setAuthState({
            token: null,
            user: null,
            isLoading: false,
          });
        }
      } catch (error) {
        console.error("Error loading auth state:", error);
        setAuthState({
          token: null,
          user: null,
          isLoading: false,
        });
      }
    };

    checkAuth();
  }, []);

  const login = (token: string, user?: User) => {
    localStorage.setItem("token", token);
    if (user) {
      localStorage.setItem("user", JSON.stringify(user));
    }

    setAuthState({
      token,
      user: user || null,
      isLoading: false,
    });
  };

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");

    setAuthState({
      token: null,
      user: null,
      isLoading: false,
    });
  };

  const updateUser = (user: User) => {
    localStorage.setItem("user", JSON.stringify(user));
    setAuthState((prev) => ({
      ...prev,
      user,
    }));
  };

  return {
    ...authState,
    login,
    logout,
    updateUser,
    isAuthenticated: !!authState.token,
  };
};
