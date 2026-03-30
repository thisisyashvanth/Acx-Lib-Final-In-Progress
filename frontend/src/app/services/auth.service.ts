import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private baseUrl = 'http://localhost:8000/auth';

  constructor(private http: HttpClient) { }

  login(req: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/login`, req);
  }

  signup(req: any) {
    return this.http.post(`${this.baseUrl}/signup`, req);
  }

  hrsignup(req: any) {
    return this.http.post(`${this.baseUrl}/hr-signup`, req);
  }

  getToken(): string | null {
    return localStorage.getItem('token');
  }

  getRole(): string | null {
    const token = this.getToken();
    if (!token) return null;

    const payload = JSON.parse(atob(token.split('.')[1]));
    return payload.role;
  }

  isHR(): boolean {
    return this.getRole() === 'HR';
  }

  isEmployee(): boolean {
    return this.getRole() === 'EMPLOYEE';
  }

  getUserId(): number | null {
    const token = this.getToken();
    if (!token) return null;

    const payload = JSON.parse(atob(token.split('.')[1]));
    return payload.user_id;
  }
}