import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ExcelService {

  constructor(private http: HttpClient) { }

  private baseUrl = `${environment.apiUrl}`;

  exportUsers(data: any[]): Observable<Blob> {
    return this.http.post(`${this.baseUrl}/hr/export-users`, data, {
      responseType: 'blob'
    });
  }

  exportRequests(data: any[]): Observable<Blob> {
    return this.http.post(`${this.baseUrl}/hr/export-requests`, data, {
      responseType: 'blob'
    });
  }

  exportBooks(data: any[]): Observable<Blob> {
    return this.http.post(`${this.baseUrl}/hr/export-books`, data, {
      responseType: 'blob'
    });
  }

  exportBookHistory(data: any[]): Observable<Blob> {
    return this.http.post(`${this.baseUrl}/hr/export-book-history`, data, {
      responseType: 'blob'
    });
  }
}
