// JavaScript pour l'admin du carrousel
document.addEventListener('DOMContentLoaded', function() {
    // Prévisualisation d'image en grand
    const imagesPreviews = document.querySelectorAll('.field-image_preview img');
    
    imagesPreviews.forEach(function(img) {
        img.addEventListener('click', function() {
            // Créer une modale simple pour voir l'image en grand
            const modal = document.createElement('div');
            modal.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.8);
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 9999;
                cursor: pointer;
            `;
            
            const modalImg = document.createElement('img');
            modalImg.src = img.src;
            modalImg.style.cssText = `
                max-width: 90%;
                max-height: 90%;
                border-radius: 8px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            `;
            
            modal.appendChild(modalImg);
            document.body.appendChild(modal);
            
            modal.addEventListener('click', function() {
                document.body.removeChild(modal);
            });
        });
    });
    
    // Validation des liens
    const lienBouton = document.querySelector('#id_lien_bouton');
    const lienInterne = document.querySelector('#id_lien_interne');
    const texteBouton = document.querySelector('#id_texte_bouton');
    
    if (lienBouton && lienInterne && texteBouton) {
        function validateButtons() {
            const hasTextBouton = texteBouton.value.trim() !== '';
            const hasLienBouton = lienBouton.value.trim() !== '';
            const hasLienInterne = lienInterne.value.trim() !== '';
            
            if (hasTextBouton && hasLienBouton && hasLienInterne) {
                alert('Attention: Vous avez renseigné un lien externe ET un lien interne. Le lien externe sera prioritaire.');
            }
        }
        
        lienBouton.addEventListener('blur', validateButtons);
        lienInterne.addEventListener('blur', validateButtons);
        texteBouton.addEventListener('blur', validateButtons);
    }
});
