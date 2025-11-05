import {
  Controller,
  Post,
  Body,
  Get,
  Patch,
  Request,
  UseGuards,
} from '@nestjs/common';
import { UserManagementService } from './user-management.service';
import { CreateUserDto } from './dto/create-user.dto';
import { LoginUserDto } from './dto/login-user.dto';
import { UpdateUserDto } from './dto/update-user.dto';
import { AuthGuard } from '@nestjs/passport';

@Controller('users')
export class UserManagementController {
  constructor(private readonly userManagementService: UserManagementService) {}

  @Post('register')
  create(@Body() createUserDto: CreateUserDto) {
    return this.userManagementService.create(createUserDto);
  }

  @Post('login')
  login(@Body() loginUserDto: LoginUserDto) {
    return this.userManagementService.login(loginUserDto);
  }

  @UseGuards(AuthGuard('jwt'))
  @Get('me')
  getProfile(@Request() req) {
    return req.user;
  }

  @UseGuards(AuthGuard('jwt'))
  @Patch('me')
  updateProfile(@Request() req, @Body() updateUserDto: UpdateUserDto) {
    return this.userManagementService.update(req.user.sub, updateUserDto);
  }
}