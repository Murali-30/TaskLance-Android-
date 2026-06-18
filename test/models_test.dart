import 'package:flutter_test/flutter_test.dart';
import 'package:tasklance/models/user.dart';
import 'package:tasklance/models/project.dart';

void main() {
  group('UserModel Tests', () {
    test('User serialization and deserialization', () {
      final user = UserModel(
        uid: 'user_1',
        name: 'Murali',
        email: 'murali123@gmail.com',
        role: UserRole.client,
        createdAt: DateTime.now(),
        skills: ['Flutter', 'Dart'],
        hourlyRate: 50.0,
      );

      final json = user.toJson();
      expect(json['uid'], 'user_1');
      expect(json['name'], 'Murali');
      expect(json['email'], 'murali123@gmail.com');
      expect(json['role'], 'client');
      expect(json['hourlyRate'], 50.0);

      final parsedUser = UserModel.fromJson(json);
      expect(parsedUser.uid, user.uid);
      expect(parsedUser.name, user.name);
      expect(parsedUser.skills, contains('Flutter'));
    });

    test('User role defaults and overrides', () {
      final client = UserModel(
        uid: 'user_1',
        name: 'Murali',
        email: 'murali123@gmail.com',
        role: UserRole.client,
        createdAt: DateTime.now(),
      );

      expect(client.role, UserRole.client);
    });
  });

  group('ProjectModel Tests', () {
    test('Project boundary values and serialization', () {
      final project = ProjectModel(
        id: 'proj_1',
        title: 'Appium Test App',
        description: 'Need automation',
        budget: 1500,
        clientUid: 'client_1',
        status: ProjectStatus.open,
        pricingType: PricingType.fixedPrice,
        startDate: DateTime.now(),
        endDate: DateTime.now().add(const Duration(days: 30)),
        createdAt: DateTime.now(),
      );

      final json = project.toJson();
      expect(json['title'], 'Appium Test App');
      expect(json['budget'], 1500);

      final parsedProject = ProjectModel.fromJson(json);
      expect(parsedProject.id, project.id);
      expect(parsedProject.title, project.title);
      expect(parsedProject.status, ProjectStatus.open);
    });
  });
}
