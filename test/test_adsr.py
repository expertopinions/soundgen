import unittest
from context import soundgen
from soundgen import *

class TestADSR(unittest.TestCase):
    def test_regular_press_time(self):
        env = adsr(1, 1, 0.5, 1, 5, 400)
        correct_env = np.concatenate([
            np.linspace(0, 1, 400),
            np.linspace(1, 0.5, 400),
            np.full(1200, 0.5),
            np.linspace(0.5, 0, 400)
        ])
        self.assertEqual(env.shape, correct_env.shape)
        self.assertTrue((env == correct_env).all())
        
    def test_attack_release_overlap(self):
        env = adsr(1, 1, 0.5, 2, .11, 400)
        correct_env = np.concatenate([
            np.linspace(0, 1, 400),
            np.linspace(1, 0, 800)
        ])
        self.assertEqual(env.shape, correct_env.shape)
        self.assertTrue((env == correct_env).all())

    def test_attack_release_boundary(self):
        env = adsr(1, 1, 0.5, 2, 1, 400)
        correct_env = np.concatenate([
            np.linspace(0, 1, 400),
            np.linspace(1, 0, 800)
        ])
        self.assertEqual(env.shape, correct_env.shape)
        self.assertTrue((env == correct_env).all())

    def test_decay_release_overlap(self):
        env = adsr(1, 1, 0.5, 2, 1.1, 400)
        correct_env = np.concatenate([
            np.linspace(0, 1, 400),
            np.linspace(1, 0.95, 40),
            np.linspace(0.95, 0, 760)
        ])
        self.assertEqual(env.shape, correct_env.shape)
        self.assertTrue((env == correct_env).all())

    def test_decay_release_boundary(self):
        env = adsr(1, 1, 0.5, 2, 2, 400)
        correct_env = np.concatenate([
            np.linspace(0, 1, 400),
            np.linspace(1, 0.5, 400),
            np.linspace(0.5, 0, 800)
        ])
        self.assertEqual(env.shape, correct_env.shape)
        self.assertTrue((env == correct_env).all())

if __name__ == '__main__':
    unittest.main()