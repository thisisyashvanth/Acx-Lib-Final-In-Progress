import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HrViewRequestHistoryComponent } from './hr-view-request-history.component';

describe('HrViewRequestHistoryComponent', () => {
  let component: HrViewRequestHistoryComponent;
  let fixture: ComponentFixture<HrViewRequestHistoryComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [HrViewRequestHistoryComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(HrViewRequestHistoryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
