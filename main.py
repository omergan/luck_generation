import datamuse_api as datamuse
import enums

if __name__ == '__main__':
    set_generated = datamuse.generate_set("find job", enums.Strength.weak)
    print(len(set_generated))
    print(set_generated)