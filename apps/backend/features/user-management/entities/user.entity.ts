export class User {
  id: string;
  name: string;
  email: string;
  password?: string;
  role: string;
  isVerified: boolean;
  createdAt: Date;
  updatedAt: Date;
}