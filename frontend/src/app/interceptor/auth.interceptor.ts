import { Injectable } from '@angular/core';
import {
  HttpEvent,
  HttpHandler,
  HttpInterceptor,
  HttpRequest
} from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {

    console.log('Interceptor hit')

    try {
      if (req.url.includes('/auth')) {
        return next.handle(req);
      }

      const token = localStorage.getItem('token');

      if (!token) {
        return next.handle(req);
      }

      const clonedReq = req.clone({
        setHeaders: {
          Authorization: `Bearer ${token}`
        }
      });

      return next.handle(clonedReq);

    } catch (error) {
      console.error('Interceptor Error:', error);
      return next.handle(req);
    }
  }
}