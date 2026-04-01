import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { UserService } from '../../../services/user.service';
import { AuthService } from '../../../services/auth.service';

@Component({
  selector: 'app-hr-navbar',
  templateUrl: './hr-navbar.component.html',
  styleUrl: './hr-navbar.component.css'
})
export class HrNavbarComponent {

  userName: string = '';

  constructor(
    private router: Router,
    private userService: UserService
  ) { }

  ngOnInit(): void {
    this.loadUser();
  }

  loadUser() {
    const token = localStorage.getItem('token');

    if (!token) {
      console.error('No token found');
      return;
    }

    const payload = JSON.parse(atob(token.split('.')[1]));
    const userId = Number(payload.sub); // ✅ FIX HERE

    console.log('UserId from token:', userId);

    this.userService.getUserById(userId).subscribe({
      next: (res: any) => {
        console.log('User API response:', res);
        this.userName = res.name;
      },
      error: (err) => {
        console.error('Failed to load user', err);
      }
    });
  }

  logout() {
    // localStorage.removeItem('token')
    localStorage.clear();
    this.router.navigate(['/signin']);
  }
}