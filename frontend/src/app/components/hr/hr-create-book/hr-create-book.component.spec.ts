import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HrCreateBookComponent } from './hr-create-book.component';

describe('HrCreateBookComponent', () => {
  let component: HrCreateBookComponent;
  let fixture: ComponentFixture<HrCreateBookComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [HrCreateBookComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(HrCreateBookComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
