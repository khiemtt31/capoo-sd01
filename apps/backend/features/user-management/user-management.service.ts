import { Injectable, UnauthorizedException } from '@nestjs/common';
import { CreateUserDto } from './dto/create-user.dto';
import { User } from './entities/user.entity';
import * as bcrypt from 'bcrypt';
import { JwtService } from '@nestjs/jwt';
import { LoginUserDto } from './dto/login-user.dto';
import { UpdateUserDto } from './dto/update-user.dto';

@Injectable()
export class UserManagementService {
  private readonly users: User[] = [];

  constructor(private readonly jwtService: JwtService) {}

  async create(createUserDto: CreateUserDto): Promise<Omit<User, 'password'>> {
    const salt = await bcrypt.genSalt();
    const hashedPassword = await bcrypt.hash(createUserDto.password, salt);

    const user: User = {
      id: (this.users.length + 1).toString(),
      ...createUserDto,
      password: hashedPassword,
      role: 'user',
      isVerified: false,
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    this.users.push(user);

    const { password, ...result } = user;
    return result;
  }

  async login(loginUserDto: LoginUserDto): Promise<{ accessToken: string }> {
    const user = this.users.find((user) => user.email === loginUserDto.email);

    if (user && (await bcrypt.compare(loginUserDto.password, user.password))) {
      const payload = { email: user.email, sub: user.id };
      return {
        accessToken: this.jwtService.sign(payload),
      };
    }
    throw new UnauthorizedException('Invalid credentials');
  }

  async update(
    id: string,
    updateUserDto: UpdateUserDto,
  ): Promise<Omit<User, 'password'>> {
    const user = this.users.find((user) => user.id === id);
    if (!user) {
      throw new UnauthorizedException('User not found');
    }

    Object.assign(user, updateUserDto);
    user.updatedAt = new Date();

    const { password, ...result } = user;
    return result;
  }
}