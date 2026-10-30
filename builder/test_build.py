"""Ensure a broken edit cannot overwrite the working release."""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class BuildValidationTest(unittest.TestCase):
    def test_invalid_javascript_preserves_release(self):
        source = Path(__file__).resolve().parent
        for broken in ('function unfinished(){', 'const duplicate=1; const duplicate=2;'):
            with self.subTest(broken=broken), tempfile.TemporaryDirectory() as directory:
                release = Path(directory)
                builder = release / 'builder'
                builder.mkdir()
                for name in ('build.py', 'template.html', 'styles.css', 'curriculum.json',
                             'snippets.json', 'challenge_snippets.json', 'extra_labs.js'):
                    shutil.copyfile(source / name, builder / name)
                (builder / 'app.js').write_text(broken)
                for name in ('index.html', 'sw.js', 'manifest.webmanifest'):
                    (release / name).write_text('working release')
                result = subprocess.run([sys.executable, str(builder / 'build.py')],
                                        capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('invalid JavaScript', result.stderr)
                for name in ('index.html', 'sw.js', 'manifest.webmanifest'):
                    self.assertEqual((release / name).read_text(), 'working release')


if __name__ == '__main__':
    unittest.main()
