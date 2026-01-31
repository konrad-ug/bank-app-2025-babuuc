import { type Page, type Locator } from '@playwright/test';

export class MfiPage {
  readonly page: Page;
  readonly pracownicyLink: Locator;
  readonly skladOsobowyLink: Locator;

  constructor(page: Page) {
    self.page = page;
    this.pracownicyLink = page.getByRole('link', { name: 'Pracownicy', exact: true });
    this.skladOsobowyLink = page.getByRole('link', { name: 'Skład osobowy' });
  }

  async goto() {
    await this.page.goto('https://mfi.ug.edu.pl/');
  }

  async goToSkladOsobowy() {
    await this.pracownicyLink.click();
    await this.skladOsobowyLink.click();
  }
}