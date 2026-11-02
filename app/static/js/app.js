// Vista previa de fotografías y captura con la cámara del dispositivo.
document.querySelectorAll('input[type="file"]').forEach((input) => {
  input.addEventListener('change', () => {
    const [file] = input.files;
    if (file) {
      showPreview(input.id, URL.createObjectURL(file));
    }
  });
});

function showPreview(kind, source) {
  const preview = document.querySelector(`[data-preview="${kind}"]`);
  preview.src = source;
  preview.hidden = false;
}

function showCameraError(kind, message) {
  const error = document.querySelector(`[data-camera-error="${kind}"]`);
  error.textContent = message;
  error.hidden = !message;
}

document.querySelectorAll('[data-camera-open]').forEach((button) => {
  button.addEventListener('click', () => openCamera(button.dataset.cameraOpen));
});

document.querySelectorAll('[data-camera-capture]').forEach((button) => {
  button.addEventListener('click', () => capturePhoto(button.dataset.cameraCapture));
});

async function openCamera(kind) {
  showCameraError(kind, '');
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    showCameraError(kind, 'Este navegador no permite usar la cámara. Sube una imagen.');
    return;
  }
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    const panel = document.querySelector(`[data-camera-panel="${kind}"]`);
    const video = panel.querySelector('video');
    video.srcObject = stream;
    await video.play();
    panel.hidden = false;
  } catch {
    showCameraError(kind, 'No pudimos acceder a la cámara. Revisa los permisos o sube una imagen.');
  }
}

function capturePhoto(kind) {
  const panel = document.querySelector(`[data-camera-panel="${kind}"]`);
  const video = panel.querySelector('video');
  const canvas = document.createElement('canvas');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext('2d').drawImage(video, 0, 0);
  canvas.toBlob((blob) => {
    const transfer = new DataTransfer();
    transfer.items.add(new File([blob], `${kind}.jpg`, { type: 'image/jpeg' }));
    const input = document.getElementById(kind);
    input.files = transfer.files;
    showPreview(kind, URL.createObjectURL(blob));
    stopCamera(panel, video);
  }, 'image/jpeg', 0.92);
}

function stopCamera(panel, video) {
  video.srcObject.getTracks().forEach((track) => track.stop());
  video.srcObject = null;
  panel.hidden = true;
}
