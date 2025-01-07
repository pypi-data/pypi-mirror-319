import unittest
import numpy as np
import pyglet
from unittest.mock import Mock, patch
from wmk.player import Player

class TestPlayer(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_frame = np.zeros((100, 100, 3), dtype=np.uint8)
        self.frame_generator = Mock(return_value=self.mock_frame)
        self.player = Player(frame_generator=self.frame_generator, width=800, height=600)

    def test_player_initialization(self) -> None:
        self.assertEqual(self.player.width, 800)
        self.assertEqual(self.player.height, 600)
        self.assertEqual(self.player.fps_max, 30)
        self.assertEqual(self.player.mouse_sensitivity, 1.0)
        self.assertIsInstance(self.player.keyboard_state, pyglet.window.key.KeyStateHandler)
        self.assertIsInstance(self.player.mouse_state, pyglet.window.mouse.MouseStateHandler)
        self.assertEqual(self.player.mouse_movement, {'dx': 0, 'dy': 0})

    def test_player_initialization_with_custom_params(self) -> None:
        player = Player(frame_generator=self.frame_generator,
                        width=1024,
                        height=768,
                        fps_max=60,
                        mouse_sensitivity=2.0)
        self.assertEqual(player.fps_max, 60)
        self.assertEqual(player.mouse_sensitivity, 2.0)
        player.close()

    @patch('pyglet.sprite.Sprite')
    def test_render_frame(self, mock_sprite: Mock) -> None:
        self.player.render_frame(self.mock_frame)
        self.assertIsNotNone(self.player.sprite)

    def test_update(self) -> None:
        self.player.update(1/30)
        self.frame_generator.assert_called_once_with(self.player, 1/30)

    @patch('pyglet.app.exit')
    def test_update_exits_on_none_frame(self, mock_exit: Mock) -> None:
        self.frame_generator.return_value = None
        self.player.update(1/30)
        mock_exit.assert_called_once()

    def test_mouse_movement_calculation(self) -> None:
        self.player._previous_mouse_x = 50
        self.player._previous_mouse_y = 75
        with patch.object(self.player, '_mouse_x', 100), patch.object(self.player, '_mouse_y', 100):
            self.player.update(1/30)
        self.assertEqual(self.player.mouse_movement['dx'], 50)
        self.assertEqual(self.player.mouse_movement['dy'], 25)

    @patch('pyglet.app.run')
    def test_run(self, mock_run: Mock) -> None:
        result = self.player.run()
        mock_run.assert_called_once()
        self.assertFalse(result)

    def tearDown(self) -> None:
        self.player.close()

if __name__ == '__main__':
    unittest.main()
