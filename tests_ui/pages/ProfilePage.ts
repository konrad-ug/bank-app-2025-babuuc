import { type Page, type Locator, expect } from '@playwright/test';

export class ProfilePage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  async expectRoomNumber(room: string) {
    await expect(this.page.getByText(`Nr pokoju: ${room}`)).toBeVisible();
  }

  async expectInstitute(instituteName: string) {
    await expect(this.page.getByText(instituteName)).toBeVisible();
  }
}