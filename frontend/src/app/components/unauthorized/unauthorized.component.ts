import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-unauthorized',
  templateUrl: './unauthorized.component.html',
  styleUrl: './unauthorized.component.css'
})
export class UnauthorizedComponent {

  constructor(private router: Router, private authService: AuthService) { }

  goToDashboard() {
    const role = this.authService.getRole();

    if (role === 'HR') {
      this.router.navigate(['/hr-dashboard']);
    } else if (role === 'EMPLOYEE') {
      this.router.navigate(['/employee-dashboard']);
    } else if (role === 'ADMIN') {
      this.router.navigate(['/admin-dashboard']);
    } else {
      this.router.navigate(['/signin']);
    }
  }

}
