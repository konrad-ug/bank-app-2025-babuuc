import { type Page, type Locator, expect } from '@playwright/test';

export class EmployeesPage {
  readonly page: Page;
  readonly searchInput: Locator;

  constructor(page: Page) {
    this.page = page;
    this.searchInput = page.getByPlaceholder('Szukaj').or(page.locator('input[type="text"]')).first();
  }

  async searchPerson(name: string) {
    await this.searchInput.fill(name);
    await this.searchInput.press('Enter');
  }

  async openProfile(fullName: string) {
    const link = this.page.getByRole('link', { name: fullName });
    await expect(link).toBeVisible();
    await link.click();
  }
}