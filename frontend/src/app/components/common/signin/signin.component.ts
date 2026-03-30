import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../../services/auth.service';

@Component({
  selector: 'app-signin',
  templateUrl: './signin.component.html',
  styleUrl: './signin.component.css'
})
export class SigninComponent {

  loginForm: FormGroup;
  loading: boolean = false;
  errorMessage: string = '';

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private authService: AuthService
  ) {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required]]
    });
  }

  onSubmit() {
    if (this.loginForm.invalid) return;

    this.loading = true;
    this.errorMessage = '';

    const payload = this.loginForm.value;

    this.authService.login(payload)
      .subscribe({

        next: (res: any) => {
          localStorage.setItem('token', res.access_token);
          this.loading = false;

          if (this.authService.isHR()) {
            this.router.navigate(['/hr-dashboard']);
          } else if (this.authService.isEmployee()) {
            this.router.navigate(['/employee-dashboard']);
          } else {
            this.errorMessage = 'Invalid Role';
          }
        },
        error: (err) => {
          this.loading = false;

          if (err.status === 401) {
            this.errorMessage = 'Invalid Email or Password';
          } else {
            this.errorMessage = err.error?.message || 'Something Went Wrong';
          }
        }
      });
  }
}