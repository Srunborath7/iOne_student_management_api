"""
Comprehensive tests for OOP architecture, Token Generation, and Authentication.
Using standard library unittest.
"""
import unittest
from app.core.security import (
    IPasswordHasher,
    BcryptPasswordHasher,
    ITokenService,
    JWTTokenService,
)
from app.repositories.base import IRepository, InMemoryRepository
from app.repositories.user import IUserRepository, UserRepository
from app.domain.user.model import User
from app.domain.user.schema import RegisterRequest, LoginRequest
from app.services.auth import IAuthService, AuthService
from app.core.exceptions import Conflict, Unauthorized


class TestOOPAuthAndToken(unittest.TestCase):
    def test_oop_hasher_polymorphism(self):
        hasher: IPasswordHasher = BcryptPasswordHasher()
        hashed = hasher.hash("secret_password")
        self.assertNotEqual(hashed, "secret_password")
        self.assertTrue(hasher.verify("secret_password", hashed))
        self.assertFalse(hasher.verify("wrong_password", hashed))

    def test_oop_token_service_generation_and_decoding(self):
        token_svc: ITokenService = JWTTokenService(secret_key="unit-test-secret-key")
        token = token_svc.create_access_token(
            subject=42,
            claims={"username": "tester", "role": "admin"},
        )
        self.assertIsInstance(token, str)
        self.assertGreater(len(token), 20)

        payload = token_svc.decode_token(token)
        self.assertEqual(payload["sub"], "42")
        self.assertEqual(payload["username"], "tester")
        self.assertEqual(payload["role"], "admin")
        self.assertIn("exp", payload)

    def test_oop_user_repository(self):
        hasher = BcryptPasswordHasher()
        repo: IUserRepository = UserRepository(seed=[], hasher=hasher)

        new_user = User(
            id=repo.next_id(),
            username="john_doe",
            password=hasher.hash("password123"),
            role="user",
            is_active=True,
        )
        repo.add(new_user)

        found = repo.find_by_username("john_doe")
        self.assertIsNotNone(found)
        self.assertEqual(found.username, "john_doe")

        # Case-insensitive search
        self.assertIsNotNone(repo.find_by_username("JOHN_DOE"))
        self.assertIsNone(repo.find_by_username("non_existent"))

    def test_oop_auth_service_registration_and_login(self):
        repo = UserRepository(seed=[])
        hasher = BcryptPasswordHasher()
        token_svc = JWTTokenService(secret_key="unit-test-secret-key")
        auth_svc: IAuthService = AuthService(
            repository=repo,
            token_mgr=token_svc,
            hasher=hasher,
            expire_minutes=60,
        )

        # 1. Register
        reg_req = RegisterRequest(username="newuser", password="securepassword123")
        user = auth_svc.register(reg_req)
        self.assertEqual(user.id, 1)
        self.assertEqual(user.username, "newuser")

        # 2. Register Duplicate -> Should raise Conflict
        with self.assertRaises(Conflict):
            auth_svc.register(reg_req)

        # 3. Login with correct credentials -> Generates Token & LoginResponse
        login_req = LoginRequest(username="newuser", password="securepassword123")
        res = auth_svc.login(login_req)
        self.assertEqual(res.message, "Login successful")
        self.assertIsNotNone(res.access_token)
        self.assertEqual(res.token_type, "bearer")
        self.assertEqual(res.user.username, "newuser")

        # 4. Login with wrong password -> Raises Unauthorized
        with self.assertRaises(Unauthorized):
            auth_svc.login(LoginRequest(username="newuser", password="wrongpassword"))

        # 5. Get current user via token
        current_user = auth_svc.get_current_user(res.access_token)
        self.assertEqual(current_user.id, user.id)
        self.assertEqual(current_user.username, "newuser")

    def test_auth_service_inactive_user(self):
        repo = UserRepository(seed=[])
        hasher = BcryptPasswordHasher()
        token_svc = JWTTokenService(secret_key="unit-test-secret-key")
        auth_svc = AuthService(
            repository=repo,
            token_mgr=token_svc,
            hasher=hasher,
        )

        inactive_user = User(
            id=repo.next_id(),
            username="disabled_user",
            password=hasher.hash("pass12345"),
            role="user",
            is_active=False,
        )
        repo.add(inactive_user)

        with self.assertRaises(Unauthorized):
            auth_svc.login(LoginRequest(username="disabled_user", password="pass12345"))


if __name__ == "__main__":
    unittest.main()
