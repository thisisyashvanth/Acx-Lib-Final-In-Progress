import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HrViewUserHistoryComponent } from './hr-view-user-history.component';

describe('HrViewUserHistoryComponent', () => {
  let component: HrViewUserHistoryComponent;
  let fixture: ComponentFixture<HrViewUserHistoryComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [HrViewUserHistoryComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(HrViewUserHistoryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
