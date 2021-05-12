"""module permettant de créer à partir d'un texte un fichier audio (text to speech) """
import requests
import time
import argparse
import logging
import json


def create_new_clip(titre, texte, voix):
  """
  permet de créer un nouveau clip à partir d'un texte et d'un titre
  :param titre: le titre du clip
  :param texte: le texte que l'on souhaite convertir en audio
  :param voix: la voix qu'on souhaite utiliser
  :return clip_id: l'id du clip audio créer
  """
  data = {
    "data": {
      "title": titre,
      "body": texte,
      "voice": voix
    },
    "callback_uri": "https://webhook.site/c4e20a8a-217f-4d9e-b6a2-de4094c99dfa"
  }
  r = requests.post(f"https://app.resemble.ai/api/v1/projects/{project}/clips",
                    headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {bearer}'},
                    json=data)
  try:
    clip_id = r.json()['id']
    logging.info(f"clip créer sous l'id: {clip_id} dans le projet avec l'id: {r.json()['project_id']}")
    return clip_id
  except json.decoder.JSONDecodeError:
    logging.error(f"Erreur lors de l'éxécution de la requête POST, code retour: {r.status_code}")
    exit(1)


def get_url_clip(clip_id, project_uuid):
  """
  méthode permettant de récupérer le lien du fichier du clip que l'on souhaite télécharger
  :param clip_id: l'id du clip
  :param project_uuid: l'uuid du projet
  :return link: l'url du fichier du clip
  """
  r = requests.get(f"https://app.resemble.ai/api/v1/projects/{project_uuid}/clips/{clip_id}",
                   headers={'Authorization': token})
  print(r.json())
  try:
    link = r.json()['link']
    logging.info(f"Lien du clip récupérer: {link}")
    return link
  except json.decoder.JSONDecodeError:
    logging.error(f"Erreur lors de la récupération de l'url du clip', code retour: {r.status_code}")
    exit(1)


def download_clip(clip_link, titre, output_path):
  r = requests.get(clip_link)
  if r.status_code == 200:
    with open(f"{output_path}/{titre}.mp3", 'wb') as f:
      f.write(r.content)
      logging.info(f"clip enregistré sous: {output_path}/{titre}.mp3")
  else:
    logging.error("Erreur lors du téléchargement du clip, vérifiez que l'argument output_path soit un chemin valide")
    exit(1)


if __name__ == '__main__':
  # gestion des arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('-te', '--texte', action="store", help="texte à convertir en audio", required=True)
  parser.add_argument('-ti', '--titre', action="store", help="titre que l'on souhaite donner au clip", required=True)
  parser.add_argument('-to', '--token', action="store", help="token de l'API pour l'authentification", required=True)
  parser.add_argument('-p', '--project_name', action="store", help="nom du projet de l'API", required=True)
  parser.add_argument('-b', '--bearer', action="store", help="Bearer de l'API pour l'authentification", required=True)
  parser.add_argument('-v', '--voice_uuid', action="store", help="l'UUID de la voice qu'on souhaite utiliser", required=True)
  parser.add_argument('-o', '--output_path', action="store", help= "Path du répértoire de sortie du fichier", required=True)
  args = parser.parse_args()

  # création des variables d'authentification
  project = args.project_name
  bearer = args.bearer
  token = args.token

  # création du nouveau clip
  clip_id = create_new_clip(args.titre, args.texte, args.voice_uuid)

  time.sleep(10)

  # récupération de l'url du clip
  clip_link = get_url_clip(clip_id, args.project_name)

  # téléchargement du fichier
  download_clip(clip_link, args.titre, args.output_path)









