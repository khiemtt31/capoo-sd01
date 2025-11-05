import { Module } from '@nestjs/common';
import { UserManagementController } from './user-management.controller';
import { UserManagementService } from './user-management.service';
import { JwtModule } from '@nestjs/jwt';
import { JwtStrategy } from '../../core/guards/jwt.strategy';

@Module({
  imports: [
    JwtModule.register({
      secret: 'yourSecretKey', // In a real app, use a config service
      signOptions: { expiresIn: '60m' },
    }),
  ],
  controllers: [UserManagementController],
  providers: [UserManagementService, JwtStrategy],
})
export class UserManagementModule {}