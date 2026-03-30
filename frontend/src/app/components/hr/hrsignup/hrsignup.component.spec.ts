import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HrsignupComponent } from './hrsignup.component';

describe('HrsignupComponent', () => {
  let component: HrsignupComponent;
  let fixture: ComponentFixture<HrsignupComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [HrsignupComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(HrsignupComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
