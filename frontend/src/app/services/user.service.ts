import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  // private baseUrl = 'http://localhost:8000/users';
  private baseUrl = `${environment.apiUrl}/users`

  constructor(private http: HttpClient) { }

  getMyBooks(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/books`);
  }

  getAllUsers(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/get-all`);
  }

  getUserHistory(userId: number) {
    return this.http.get(`${this.baseUrl}/${userId}/history`);
  }

  getUserById(userId: number) {
    return this.http.get(`${this.baseUrl}/${userId}`);
  }
}