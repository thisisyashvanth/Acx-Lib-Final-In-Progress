import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HrGetAllUsersComponent } from './hr-get-all-users.component';

describe('HrGetAllUsersComponent', () => {
  let component: HrGetAllUsersComponent;
  let fixture: ComponentFixture<HrGetAllUsersComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [HrGetAllUsersComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(HrGetAllUsersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
