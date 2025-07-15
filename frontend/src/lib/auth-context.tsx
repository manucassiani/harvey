import React, { createContext, useContext, useEffect, useState } from 'react';
import { supabase } from './supabase';
import { User as SupabaseUser } from '@supabase/supabase-js';

interface User {
  id: string;
  email: string;
  is_active: boolean;
  created_at: string;
}

interface Profile {
  id: string;
  full_name: string;
  phone?: string;
  is_admin: boolean;
  is_doctor: boolean;
  avatar_url?: string;
  emergency_info?: any;
  specialty?: string;
  institution?: string;
}

interface AuthContextProps {
  user: User | null;
  profile: Profile | null;
  loading: boolean;
  signUp: (email: string, password: string, fullName: string) => Promise<void>;
  signIn: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
  error: string | null;
}

const AuthContext = createContext<AuthContextProps | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [profile, setProfile] = useState<Profile | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        // Get current user from Supabase
        const { data: { user: supabaseUser } } = await supabase.auth.getUser();
        
        if (!supabaseUser) {
          setLoading(false);
          return;
        }

        // Convert Supabase user to our User type
        const userData: User = {
          id: supabaseUser.id,
          email: supabaseUser.email!,
          is_active: true,
          created_at: supabaseUser.created_at || new Date().toISOString()
        };
        setUser(userData);

        // Get user profile from Supabase
        const { data: profileData, error: profileError } = await supabase
          .from('profiles')
          .select('*')
          .eq('id', supabaseUser.id)
          .single();

        if (profileError) {
          console.error('Error fetching profile:', profileError);
          // Try to create profile if it doesn't exist
          if (profileError.code === 'PGRST116') {
            await createUserProfile(supabaseUser);
          }
        } else {
          setProfile(profileData as Profile);
        }
      } catch (error) {
        console.error('Error fetching user data:', error);
        setError('Failed to fetch user data');
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();

    // Listen for auth changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      (event, session) => {
        if (event === 'SIGNED_IN' && session) {
          fetchUserData();
        } else if (event === 'SIGNED_OUT') {
          setUser(null);
          setProfile(null);
        }
      }
    );

    return () => {
      subscription.unsubscribe();
    };
  }, []);

  const createUserProfile = async (supabaseUser: SupabaseUser) => {
    try {
      const profileData = {
        id: supabaseUser.id,
        full_name: supabaseUser.user_metadata?.full_name || supabaseUser.email?.split('@')[0] || 'Usuario',
        is_doctor: false,
        is_admin: false,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        emergency_info: {
          allergies: [],
          conditions: [],
          medications: [],
          bloodType: '',
          medicationReminders: []
        }
      };

      const { data, error } = await supabase
        .from('profiles')
        .insert(profileData)
        .select()
        .single();

      if (error) {
        console.error('Error creating profile:', error);
      } else {
        setProfile(data as Profile);
        console.log('Profile created successfully:', data);
      }
    } catch (error) {
      console.error('Error creating profile:', error);
    }
  };

  const signUp = async (email: string, password: string, fullName: string) => {
    try {
      setLoading(true);
      setError(null);
      
      // Register user with Supabase
      const { data, error } = await supabase.auth.signUp({
        email,
        password,
        options: {
          data: {
            full_name: fullName
          }
        }
      });
      
      if (error) {
        throw error;
      }

      // Profile will be created automatically on auth state change
      
    } catch (error: any) {
      console.error('Error signing up:', error);
      setError(error.message || 'An error occurred during sign up');
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const signIn = async (email: string, password: string) => {
    try {
      setLoading(true);
      setError(null);
      
      // Login with Supabase
      const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password
      });
      
      if (error) {
        throw error;
      }

      // User and profile will be set automatically by auth state change listener
      
    } catch (error: any) {
      console.error('Error signing in:', error);
      setError(error.message || 'An error occurred during sign in');
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const signOut = async () => {
    try {
      setLoading(true);
      
      // Clear all cache on sign out
      try {
        const { dataCache } = await import('./utils');
        dataCache.clear();
      } catch (e) {
        // Ignore if utils doesn't exist
      }
      
      const { error } = await supabase.auth.signOut();
      if (error) {
        throw error;
      }
      
      setUser(null);
      setProfile(null);
    } catch (error: any) {
      console.error('Error signing out:', error);
      setError(error.message || 'An error occurred during sign out');
      throw error;
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        profile,
        loading,
        signUp,
        signIn,
        signOut,
        error,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};