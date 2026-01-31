import { test } from '@playwright/test';
import { MfiPage } from '../pages/MfiPage';
import { EmployeesPage } from '../pages/EmployeesPage';
import { ProfilePage } from '../pages/ProfilePage';

test.describe('Testy Pracowników MFI UG', () => {

  test('Zadanie 1 (Refaktor): Sprawdź pokój pracownika UG (Konrad Sołtys)', async ({ page }) => {
    const mfiPage = new MfiPage(page);
    const employeesPage = new EmployeesPage(page);
    const profilePage = new ProfilePage(page);

    await mfiPage.goto();
    await mfiPage.goToSkladOsobowy();
    
    await employeesPage.searchPerson('sołtys');
    await employeesPage.openProfile('mgr Konrad Sołtys');

    await profilePage.expectRoomNumber('4.19');
  });

  test('Zadanie 3: Sprawdź Instytut mgr Anny Baran', async ({ page }) => {
    const mfiPage = new MfiPage(page);
    const employeesPage = new EmployeesPage(page);
    const profilePage = new ProfilePage(page);

    await mfiPage.goto();
    await mfiPage.goToSkladOsobowy();

    await employeesPage.searchPerson('Anna Baran');
    await employeesPage.openProfile('mgr Anna Baran');

    await profilePage.expectInstitute('Instytut Fizyki Doświadczalnej');
  });

});