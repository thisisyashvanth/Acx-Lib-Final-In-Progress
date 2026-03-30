import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  private baseUrl = 'http://localhost:8000/users';

  constructor(private http: HttpClient) { }

  getMyBooks(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/my-books`);
  }
}
