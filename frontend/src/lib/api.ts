// API client configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

// Token management
const TOKEN_KEY = 'harvey_token';

export const getAuthToken = (): string | null => {
  return localStorage.getItem(TOKEN_KEY);
};

export const setAuthToken = (token: string): void => {
  localStorage.setItem(TOKEN_KEY, token);
};

export const clearAuthToken = (): void => {
  localStorage.removeItem(TOKEN_KEY);
};

// API client class
class ApiClient {
  private baseURL: string;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = getAuthToken();
    
    const config: RequestInit = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
      },
    };

    const response = await fetch(`${this.baseURL}${endpoint}`, config);

    if (!response.ok) {
      if (response.status === 401) {
        clearAuthToken();
        window.location.href = '/';
      }
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  // Auth endpoints
  async login(email: string, password: string) {
    const response = await this.request<{ access_token: string; token_type: string }>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    
    setAuthToken(response.access_token);
    return response;
  }

  async register(email: string, password: string) {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  async logout() {
    await this.request('/auth/logout', { method: 'POST' });
    clearAuthToken();
  }

  async getCurrentUser() {
    return this.request('/auth/me');
  }

  async getCurrentUserProfile() {
    return this.request('/auth/me/profile');
  }

  async checkEmailWhitelist(email: string) {
    return this.request('/auth/check-email', {
      method: 'POST',
      body: JSON.stringify({ email }),
    });
  }

  // Profile endpoints
  async createProfile(profile: any) {
    return this.request('/profiles', {
      method: 'POST',
      body: JSON.stringify(profile),
    });
  }

  async updateProfile(profile: any) {
    return this.request('/profiles', {
      method: 'PUT',
      body: JSON.stringify(profile),
    });
  }

  async getProfile(userId: string) {
    return this.request(`/profiles/${userId}`);
  }

  async getDoctors() {
    return this.request('/profiles/doctors/list');
  }

  async uploadAvatar(file: File) {
    const formData = new FormData();
    formData.append('file', file);
    
    const token = getAuthToken();
    const response = await fetch(`${this.baseURL}/profiles/avatar`, {
      method: 'POST',
      headers: {
        ...(token && { Authorization: `Bearer ${token}` }),
      },
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  // Appointments endpoints
  async createAppointment(appointment: any) {
    return this.request('/appointments', {
      method: 'POST',
      body: JSON.stringify(appointment),
    });
  }

  async getAppointments() {
    return this.request('/appointments');
  }

  async getUpcomingAppointments() {
    return this.request('/appointments/upcoming');
  }

  async getPastAppointments() {
    return this.request('/appointments/past');
  }

  async getAppointment(appointmentId: string) {
    return this.request(`/appointments/${appointmentId}`);
  }

  async updateAppointment(appointmentId: string, appointment: any) {
    return this.request(`/appointments/${appointmentId}`, {
      method: 'PUT',
      body: JSON.stringify(appointment),
    });
  }

  async deleteAppointment(appointmentId: string) {
    return this.request(`/appointments/${appointmentId}`, {
      method: 'DELETE',
    });
  }

  // Consultations endpoints
  async createConsultation(consultation: any) {
    return this.request('/consultations', {
      method: 'POST',
      body: JSON.stringify(consultation),
    });
  }

  async getConsultations() {
    return this.request('/consultations');
  }

  async getConsultation(consultationId: string) {
    return this.request(`/consultations/${consultationId}`);
  }

  async getConsultationByShare(shareHash: string) {
    return this.request(`/consultations/share/${shareHash}`);
  }

  async updateConsultation(consultationId: string, consultation: any) {
    return this.request(`/consultations/${consultationId}`, {
      method: 'PUT',
      body: JSON.stringify(consultation),
    });
  }

  async uploadConsultationAudio(consultationId: string, file: File) {
    const formData = new FormData();
    formData.append('file', file);
    
    const token = getAuthToken();
    const response = await fetch(`${this.baseURL}/consultations/${consultationId}/audio`, {
      method: 'POST',
      headers: {
        ...(token && { Authorization: `Bearer ${token}` }),
      },
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  // Transcriptions endpoints
  async createTranscription(transcription: any) {
    return this.request('/transcriptions', {
      method: 'POST',
      body: JSON.stringify(transcription),
    });
  }

  async getTranscriptionByConsultation(consultationId: string) {
    return this.request(`/transcriptions/consultation/${consultationId}`);
  }

  async getTranscription(transcriptionId: string) {
    return this.request(`/transcriptions/${transcriptionId}`);
  }

  // Summaries endpoints
  async createSummary(summary: any) {
    return this.request('/summaries', {
      method: 'POST',
      body: JSON.stringify(summary),
    });
  }

  async getSummariesByConsultation(consultationId: string) {
    return this.request(`/summaries/consultation/${consultationId}`);
  }

  async getSummaryByType(consultationId: string, type: string) {
    return this.request(`/summaries/consultation/${consultationId}/type/${type}`);
  }

  async getSummary(summaryId: string) {
    return this.request(`/summaries/${summaryId}`);
  }

  // Admin endpoints
  async addEmailToWhitelist(email: string, notes?: string) {
    return this.request('/admin/whitelist', {
      method: 'POST',
      body: JSON.stringify({ email, notes }),
    });
  }

  async getWhitelistedEmails() {
    return this.request('/admin/whitelist');
  }

  async removeEmailFromWhitelist(emailId: string) {
    return this.request(`/admin/whitelist/${emailId}`, {
      method: 'DELETE',
    });
  }

  async getAllUsers() {
    return this.request('/admin/users');
  }

  async toggleAdminStatus(userId: string) {
    return this.request(`/admin/users/${userId}/admin`, {
      method: 'PUT',
    });
  }

  async toggleDoctorStatus(userId: string) {
    return this.request(`/admin/users/${userId}/doctor`, {
      method: 'PUT',
    });
  }

  async getDoctorReviews() {
    return this.request('/admin/doctor-reviews');
  }

  async approveDoctorReview(reviewId: string) {
    return this.request(`/admin/doctor-reviews/${reviewId}/approve`, {
      method: 'PUT',
    });
  }

  async rejectDoctorReview(reviewId: string, feedback: string) {
    return this.request(`/admin/doctor-reviews/${reviewId}/reject`, {
      method: 'PUT',
      body: JSON.stringify({ feedback }),
    });
  }
}

// Export singleton instance
export const api = new ApiClient(API_BASE_URL); 